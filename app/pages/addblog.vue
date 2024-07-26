<!-- eslint-disable vue/html-closing-bracket-newline -->
<!-- eslint-disable @stylistic/semi -->
<!-- eslint-disable @stylistic/comma-dangle -->
<!-- eslint-disable @stylistic/quotes -->
<script setup lang="ts">
import type { FormError, FormSubmitEvent } from "#ui/types";
import { ref, reactive } from "vue";
const toast = useToast();
definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Add Blog Post",
});

const state = reactive({
  title: "",
  content: "",
  category: "",
  images: [] as File[],
});
const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.title)
    errors.push({ path: "title", message: "Title is required" });
  if (!state.content)
    errors.push({ path: "content", message: "Content is required" });
  if (!state.category)
    errors.push({ path: "category", message: "Category is required" });
  return errors;
};

const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement;
  if (input.files) {
    state.images = Array.from(input.files);
  }
};

const accesToken = localStorage.getItem("access_token");

const addUserBlog = async (event: FormSubmitEvent<any>) => {
  console.log(accesToken);

  const formData = new FormData();
  formData.append("title", state.title);
  formData.append("content", state.content);
  formData.append("category", state.category);

  if (state.images.length > 0) {
    state.images.forEach((file) => {
      formData.append("images", file);
    });
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/blog_posts", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accesToken}`,
      },
      body: formData,
    });

    if (!response.ok) {
      // Handle error response
      const errorData = await response.json();
      console.error("Failed to add blog post:", errorData.detail);
      toast.add({
        title: "Blog post creation failed",
        description:
          errorData.detail || "An error occurred while creating the blog post.",
        timeout: 1000,
      });
      return;
    }

    const result = await response.json(); // Get the response JSON
    console.log(result);
    await navigateTo({ path: "/blogs" });
    toast.add({
      title: "Blog post created successfully",
      timeout: 1000,
    });
  } catch (error) {
    console.error("Error during fetch:", error);
    toast.add({
      title: "Blog post creation failed",
      description: "An unexpected error occurred. Please try again.",
      timeout: 1000,
    });
  }
};
</script>

<!-- eslint-disable vue/multiline-html-element-content-newline -->
<!-- eslint-disable vue/singleline-html-element-content-newline -->
<template>
  <UCard class="max-w-sm w-full bg-white/75 dark:bg-white/5 backdrop-blur">
    <UForm
      :validate="validate"
      :state="state"
      class="space-y-4"
      @submit="addUserBlog"
    >
      <UFormGroup label="Title" name="title">
        <UInput v-model="state.title" />
      </UFormGroup>

      <UFormGroup label="Category" name="category">
        <USelect
          v-model="state.category"
          :options="[
            'Computer Science',
            'Technology',
            'Software Engineering',
            'Programming',
          ]"
        />
      </UFormGroup>

      <UFormGroup label="Content" name="content">
        <UTextarea v-model="state.content" />
      </UFormGroup>

      <UFormGroup label="Images" name="images">
        <input
          type="file"
          multiple
          @change="handleFileChange"
          accept="image/*"
          class="form-input mt-1 block w-full"
        />
      </UFormGroup>

      <UButton block type="submit"> Add Blog Post </UButton>
    </UForm>
  </UCard>
</template>
