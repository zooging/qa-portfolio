const { test, expect } = require('@playwright/test');
const { login, addProduct } = require('./helpers');

test.describe('Корзина', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('добавление товара обновляет счётчик', async ({ page }) => {
    await addProduct(page, 'sauce-labs-backpack');

    await expect(page.locator('.shopping_cart_badge')).toHaveText('1');
    await expect(page.locator('#remove-sauce-labs-backpack')).toBeVisible();
  });

  test('товар можно удалить из корзины', async ({ page }) => {
    await addProduct(page, 'sauce-labs-backpack');
    await page.locator('.shopping_cart_link').click();
    await expect(page.locator('.cart_item')).toHaveCount(1);

    await page.locator('#remove-sauce-labs-backpack').click();

    await expect(page.locator('.cart_item')).toHaveCount(0);
  });

  test('корзина сохраняется после перезагрузки страницы', async ({ page }) => {
    await addProduct(page, 'sauce-labs-bike-light');
    await addProduct(page, 'sauce-labs-backpack');

    await page.reload();

    await expect(page.locator('.shopping_cart_badge')).toHaveText('2');
  });

  test('кнопка Continue shopping возвращает в каталог', async ({ page }) => {
    await addProduct(page, 'sauce-labs-backpack');
    await page.locator('.shopping_cart_link').click();

    await page.locator('#continue-shopping').click();

    await expect(page).toHaveURL(/\/inventory\.html$/);
  });
});
