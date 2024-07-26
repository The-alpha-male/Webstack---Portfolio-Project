<!-- eslint-disable @stylistic/semi -->
<!-- eslint-disable @stylistic/comma-dangle -->
<!-- eslint-disable @stylistic/quotes -->
<script setup>
import { ref, onMounted } from "vue";
import { createError } from "nuxt/app"; // Import createError properly

// import { ref, computed, onMounted } from "vue";

const posts = ref([]);

// import type { BlogPost } from "~/types";

// const { data: page } = await useAsyncData("blog", () =>
//   queryContent("/blog").findOne()
// );
// if (!page.value) {
//   throw createError({
//     statusCode: 404,
//     statusMessage: "Page not found",
//     fatal: true,
//   });
// }

// const { data: posts } = await useAsyncData("posts", () =>
//   queryContent<BlogPost>("/blog")
//     .where({ _extension: "md" })
//     .sort({ date: -1 })
//     .find()
// );

const getAPIData = async () => {
  try {
    let res = await fetch(
      "http://127.0.0.1:8000/get_all_blogs?skip=0&limit=100",
      {
        method: "GET",
      }
    );
    if (!res.ok) {
      throw new Error("Network response was not ok");
    }
    let data = await res.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch data:", error);
    throw createError({
      statusCode: 500,
      statusMessage: "Failed to fetch data",
      fatal: true,
    });
  }
};

onMounted(async () => {
  try {
    let data = await getAPIData();
    if (!data) {
      throw createError({
        statusCode: 404,
        statusMessage: "Page not found",
        fatal: true,
      });
    }
    posts.value = data;
  } catch (error) {
    console.error("Error in onMounted:", error);
  }
});

// useSeoMeta({
//   title: page.value.title,
//   ogTitle: page.value.title,
//   description: page.value.description,
//   ogDescription: page.value.description,
// });

// defineOgImage({
//   component: "Saas",
//   title: page.value.title,
//   description: page.value.description,
// });
</script>

<template>
  <UContainer>
    <!-- {{ posts }} -->
    <UPageHeader :posts="posts" class="py-[50px]" />

    <UPageBody>
      <UBlogList orientation="horizontal">
        <UBlogPost
          v-for="(post, index) in posts"
          :key="post.id"
          :title="post.title"
          :description="post.content"
          :image="
            post.images && post.images.length > 0
              ? `http://${post.images[0].image_url}`
              : 'https://images.unsplash.com/photo-1640161704729-cbe966a08476?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
          "
          :date="
            new Date(post.created_at).toLocaleDateString('en', {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
            })
          "
          :authors="[
            {
              name: post.author,
              avatar: {
                src: 'https://github.com/danielroe.png',
                target: '_blank',
              },
              to: 'https://twitter.com/danielcroe',
            },
          ]"
          :badge="{ label: post.category }"
          :orientation="index === 0 ? 'horizontal' : 'vertical'"
          :class="[index === 0 ? 'col-span-full' : '']"
          :ui="{ description: 'line-clamp-2' }"
        />
      </UBlogList>
    </UPageBody>
  </UContainer>
</template>
