const { test, expect } = require('@playwright/test');
const { login, addProduct } = require('./helpers');

test.describe('Оформление заказа', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await addProduct(page, 'sauce-labs-backpack');
    await page.locator('.shopping_cart_link').click();
    await page.locator('#checkout').click();
  });

  test('полный сценарий заказа завершается подтверждением', async ({ page }) => {
    await page.locator('#first-name').fill('Dmitry');
    await page.locator('#last-name').fill('Borisov');
    await page.locator('#postal-code').fill('634000');
    await page.locator('#continue').click();

    await expect(page.locator('.summary_total_label')).toBeVisible();

    await page.locator('#finish').click();

    await expect(page.locator('.complete-header')).toHaveText('Thank you for your order!');
  });

  test('пустые обязательные поля блокируют оформление', async ({ page }) => {
    await page.locator('#continue').click();

    await expect(page.locator('[data-test="error"]')).toContainText('First Name is required');
  });

  test('отмена возвращает в корзину', async ({ page }) => {
    await page.locator('#cancel').click();

    await expect(page).toHaveURL(/\/cart\.html$/);
    await expect(page.locator('.cart_item')).toHaveCount(1);
  });
});
