<!-- eslint-disable @stylistic/semi -->
<!-- eslint-disable @stylistic/comma-dangle -->
<!-- eslint-disable @stylistic/quotes -->
<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { createError } from "nuxt/app"; // Import createError properly

const post = ref(null);
const route = useRoute();
const router = useRouter();

const getPostData = async (id) => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/blog_posts/${id}`, {
      method: "GET",
    });
    if (!res.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await res.json();
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
    const data = await getPostData(route.params.id);
    if (!data) {
      throw createError({
        statusCode: 404,
        statusMessage: "Post not found",
        fatal: true,
      });
    }
    post.value = data;
  } catch (error) {
    console.error("Error in onMounted:", error);
  }
});
const items = [
  "https://picsum.photos/600/600?random=1",
  "https://picsum.photos/600/600?random=2",
  "https://picsum.photos/600/600?random=3",
  "https://picsum.photos/600/600?random=4",
  "https://picsum.photos/600/600?random=5",
  "https://picsum.photos/600/600?random=6",
];
</script>

<template>
  <UContainer v-if="post">
    <UBlogPost
      :title="post.title"
      :description="post.content"
      :date="
        new Date(post.created_at).toLocaleDateString('en', {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
        })
      "
      orientation="horizontal"
      :image="
        post.images && post.images.length > 0
          ? `http://${post.images[0].image_url}`
          : 'https://images.unsplash.com/photo-1640161704729-cbe966a08476?q=80&w=2072&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
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
    />
  </UContainer>
</template>
