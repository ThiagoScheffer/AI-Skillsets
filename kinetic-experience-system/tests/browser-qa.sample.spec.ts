/**
 * OPTIONAL Playwright test template; not executed by the Python unit test suite.
 * Adapt routes, headings and selectors to the host application's actual UI.
 * Requires a configured @playwright/test project and running dev server.
 */
import { test, expect } from "@playwright/test";

test.describe("KX route transitions", () => {
  test("deep link remains accessible without animated origin", async ({ page }) => {
    await page.goto("/work/example-project");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await expect(page.locator("[data-kx-blocking-overlay]")).toHaveCount(0);
  });

  test("navigation back returns to the correct route", async ({ page }) => {
    await page.goto("/work");
    await page.getByRole("link", { name: /example project/i }).click();
    await expect(page).toHaveURL(/\/work\/example-project/);
    await page.goBack();
    await expect(page).toHaveURL(/\/work$/);
  });

  test("reduced motion keeps content visible", async ({ page }) => {
    await page.emulateMedia({ reducedMotion: "reduce" });
    await page.goto("/work/example-project");
    await expect(page.getByRole("main")).toBeVisible();
  });
});
