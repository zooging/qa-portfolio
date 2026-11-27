const { test, expect } = require('@playwright/test');
const { login } = require('./helpers');

test.describe('Авторизация', () => {
  test('валидные данные открывают каталог', async ({ page }) => {
    await login(page);

    await expect(page.locator('.inventory_item')).toHaveCount(6);
    await expect(page.locator('.title')).toHaveText('Products');
  });

  test('неверный пароль показывает ошибку', async ({ page }) => {
    await page.goto('/');
    await page.locator('#user-name').fill('standard_user');
    await page.locator('#password').fill('wrong-password');
    await page.locator('#login-button').click();

    await expect(page.locator('[data-test="error"]')).toContainText(
      'Username and password do not match'
    );
    await expect(page.locator('#user-name')).toBeVisible();
  });

  test('заблокированный пользователь не входит', async ({ page }) => {
    await page.goto('/');
    await page.locator('#user-name').fill('locked_out_user');
    await page.locator('#password').fill('secret_sauce');
    await page.locator('#login-button').click();

    await expect(page.locator('[data-test="error"]')).toContainText('locked out');
    await expect(page).not.toHaveURL(/inventory/);
  });

  test('logout возвращает на форму входа', async ({ page }) => {
    await login(page);
    await page.locator('#react-burger-menu-btn').click();
    await page.locator('#logout_sidebar_link').click();

    await expect(page.locator('#login-button')).toBeVisible();
    await expect(page).toHaveURL('https://www.saucedemo.com/');
  });
});
