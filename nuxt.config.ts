// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  extends: [process.env.NUXT_UI_PRO_PATH || "@nuxt/ui-pro"],

  modules: [
<<<<<<< HEAD
    '@nuxt/content',
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/ui',
    '@nuxt/fonts',
    '@nuxthq/studio',
    '@vueuse/nuxt',
    'nuxt-og-image',
    'nuxt-vue3-google-signin' // Added Google Sign-In module
=======
    "@nuxt/content",
    "@nuxt/eslint",
    "@nuxt/image",
    "@nuxt/ui",
    "@nuxt/fonts",
    "@nuxthq/studio",
    "@vueuse/nuxt",
    "nuxt-og-image",
    // "vuetify-nuxt-module"
>>>>>>> 36534160b6baa96712b9a317c2fc59db396f9891
  ],

  googleSignIn: {
    clientId: 'CLIENT ID OBTAINED FROM GOOGLE API CONSOLE', // Added Google Sign-In configuration
  },

  hooks: {
    // Define `@nuxt/ui` components as global to use them in `.md` (feel free to add those you need)
    "components:extend": (components) => {
      const globals = components.filter((c) =>
        ["UButton"].includes(c.pascalName)
      );

      globals.forEach((c) => (c.global = true));
    },
  },

  ui: {
    icons: ["heroicons", "simple-icons"],
  },

  colorMode: {
    disableTransition: true,
  },

  routeRules: {
    "/": { redirect: "/news", prerender: false },
  },

  devtools: {
    enabled: true,
  },

  typescript: {
    strict: false,
  },

  future: {
    compatibilityVersion: 4,
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: "never",
        braceStyle: "1tbs",
      },
    },
  },

<<<<<<< HEAD
  compatibilityDate: '2024-07-11'
})
=======
  compatibilityDate: "2024-07-11",
});
>>>>>>> 36534160b6baa96712b9a317c2fc59db396f9891
