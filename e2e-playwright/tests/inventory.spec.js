const { test, expect } = require('@playwright/test');
const { login } = require('./helpers');

test.describe('Каталог', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('отображаются все 6 товаров', async ({ page }) => {
    await expect(page.locator('.inventory_item')).toHaveCount(6);
    await expect(page.locator('.inventory_item_name').first()).toBeVisible();
  });

  test('сортировка по цене по возрастанию', async ({ page }) => {
    await page.locator('[data-test="product-sort-container"]').selectOption('lohi');

    const prices = await page.locator('.inventory_item_price').allTextContents();
    const numbers = prices.map((value) => Number(value.replace('$', '')));
    expect(numbers).toEqual([...numbers].sort((a, b) => a - b));
  });

  test('сортировка по названию по убыванию', async ({ page }) => {
    await page.locator('[data-test="product-sort-container"]').selectOption('za');

    const names = await page.locator('.inventory_item_name').allTextContents();
    expect(names).toEqual([...names].sort((a, b) => b.localeCompare(a)));
  });

  test('карточка товара открывается и возвращает в каталог', async ({ page }) => {
    await page.locator('.inventory_item_name').first().click();

    await expect(page.locator('.inventory_details_name')).toBeVisible();
    await expect(page.locator('.inventory_details_desc')).not.toBeEmpty();
    await expect(page.locator('.inventory_details_price')).toBeVisible();

    await page.locator('#back-to-products').click();
    await expect(page).toHaveURL(/\/inventory\.html$/);
  });
});
