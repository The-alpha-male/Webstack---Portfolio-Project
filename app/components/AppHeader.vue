<script setup lang="ts">
import type { NavItem } from "@nuxt/content";

const navigation = inject<Ref<NavItem[]>>("navigation", ref([]));

const links = [
  {
    label: "News",
    to: "/news",
  },

  {
    label: "Blogs",
    to: "/blogs",
  },
];
</script>

<template>
  <UHeader :links="links">
    <template #logo>
      &lt;/CodeHatari &gt;
      <UBadge label="</CH>" variant="subtle" class="mb-0.5" />
    </template>

    <template #right>
      <UButton label="Sign in" color="gray" to="/login" />
      <UButton
        label="Sign up"
        icon="i-heroicons-arrow-right-20-solid"
        trailing
        color="black"
        to="/signup"
        class="hidden lg:flex"
      />
    </template>

    <template #panel>
      <UNavigationTree :links="mapContentNavigation(navigation)" default-open />
    </template>
  </UHeader>
</template>
