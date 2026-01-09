from playwright.async_api import async_playwright, Page, Locator, TimeoutError as PlaywrightTimeoutError
from kasawa import console
import asyncio

async def click_by_mouse(page: Page, locator: Locator):
    bbox = await locator.bounding_box()
    if bbox:
        x = bbox["x"] + bbox["width"] / 2
        y = bbox["y"] + bbox["height"] / 2
        await page.mouse.click(x, y)
    else:
        console.log.error("[Box] Not found Your Box !")

checkbox_selector = "//iframe[starts-with(@src,'https://newassets.hcaptcha.com/captcha/v1/') and contains(@src, 'frame=checkbox')]"

async def click_checkbox(page: Page, timeout: int = 10000, retry: int = 2):
    for attempt in range(retry):
        try:
            checkbox_frame = page.frame_locator(checkbox_selector)
            checkbox_element = checkbox_frame.locator("//div[@id='checkbox']")
            await checkbox_element.wait_for(state="visible", timeout=timeout)
            await click_by_mouse(page, checkbox_element)
            return True
        except PlaywrightTimeoutError:
            await asyncio.sleep(1)
    return False
