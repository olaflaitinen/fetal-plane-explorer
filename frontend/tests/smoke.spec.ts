import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/Fetal Plane Explorer/);
});

test('shows upload area', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText('Drag & Drop Ultrasound Image Here')).toBeVisible();
});
