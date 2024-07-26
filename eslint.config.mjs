// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt({
  rules: {
    "@typescript-eslint/no-explicit-any": "off",
    // quotes: ["error", "single", { avoidEscape: true }],
    quotes: "off",
  },
});
