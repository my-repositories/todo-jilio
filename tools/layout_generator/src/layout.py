"""Модуль для асинхронной параллельной генерации UI/UX макетов через Hugging Face API."""

import asyncio
import os
import sys
from huggingface_hub import InferenceClient
from PIL import Image

MODEL_NAME: str = "black-forest-labs/FLUX.1-schnell"


def get_inference_client() -> InferenceClient:
    """Проверяет наличие токена и возвращает клиент Hugging Face."""
    hf_token: str | None = os.getenv("HF_TOKEN")
    if not hf_token:
        print(
            "❌ Ошибка: Переменная окружения HF_TOKEN не задана!",
            file=sys.stderr,
        )
        print(
            "👉 Запуск: HF_TOKEN='твой_токен' uv run layout.py",
            file=sys.stderr,
        )
        sys.exit(1)
    return InferenceClient(token=hf_token)


def sync_generate_image(
    client: InferenceClient, prompt: str, width: int, height: int
) -> Image.Image:
    """Синхронный рабочий метод для отправки запроса в API."""
    full_prompt: str = (
        "Figma UI UX design template, "
        + prompt
        + ", crisp detail, professional software interface, 4k sharp focus"
    )
    return client.text_to_image(
        prompt=full_prompt,
        model=MODEL_NAME,
        width=width,
        height=height,
    )


async def generate_and_save_task(
    client: InferenceClient,
    prompt: str,
    size: tuple[int, int],
    filename: str,
    log_prefix: str,
) -> None:
    """Асинхронная задача: запускает генерацию в отдельном потоке и сохраняет результат."""
    width, height = size
    print(log_prefix + " Начало генерации (" + str(width) + "x" + str(height) + ")...")

    try:
        img: Image.Image = await asyncio.to_thread(
            sync_generate_image, client, prompt, width, height
        )

        await asyncio.to_thread(img.save, filename, "PNG")
        print("✅ " + log_prefix + " Успешно сохранен в " + filename)

    except RuntimeError as e:
        print(
            "❌ " + log_prefix + " Ошибка выполнения: " + str(e),
            file=sys.stderr,
        )


async def main_async() -> None:
    """Параллельный запуск генерации десктопной и мобильной версий."""
    client: InferenceClient = get_inference_client()

    core_ui_prompt: str = (
        "flat web app interface design for 'Jilio' todo list application, "
        "modern Google Material 3 Design UI style. Features clean Material 3 "
        "Outlined text fields for title and description with an explicit "
        "'No Date / Без даты' checkbox. The layout includes a segmented control "
        "for priority filtering: 'All', 'Regular', 'Important', 'Critical'. "
        "Task list cards show edit and delete icon buttons, checkbox toggles, "
        "and colorful category chips. One completed task is checked and faded. "
        "One task is highlighted with a striking Material 3 error-state red "
        "border and an explicit overdue warning badge."
    )

    desktop_prompt: str = (
        core_ui_prompt
        + ", professional desktop web dashboard layout, left navigation rail "
        "and sidebar drawer containing task groups like 'Work' and 'Personal', "
        "widescreen design grid with soft elevation shadows"
    )
    mobile_prompt: str = (
        core_ui_prompt
        + ", native Android mobile app appearance, bezel-less smartphone viewport, "
        "top app bar with task counters, a horizontal scrollable row of Material "
        "filter chips for categories under the header, and a prominent round "
        "Floating Action Button (FAB) for adding tasks at the bottom right corner"
    )

    print("🚀 Запуск асинхронной параллельной генерации на серверах Hugging Face...")

    await asyncio.gather(
        generate_and_save_task(
            client, desktop_prompt, (1280, 800), "desktop.png", "🖥️  [Desktop]"
        ),
        generate_and_save_task(
            client, mobile_prompt, (512, 1024), "mobile.png", "📱 [Mobile]"
        ),
    )

    print("🎉 Все параллельные задачи завершены!")


def main() -> None:
    """Точка входа."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
