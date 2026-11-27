const { expect } = require('@playwright/test');

async function login(page, user = 'standard_user', password = 'secret_sauce') {
  await page.goto('/');
  await page.locator('#user-name').fill(user);
  await page.locator('#password').fill(password);
  await page.locator('#login-button').click();
  await expect(page).toHaveURL(/\/inventory\.html$/);
}

async function addProduct(page, productId) {
  await page.locator(`[data-test="add-to-cart-${productId}"]`).click();
}

module.exports = { login, addProduct };
