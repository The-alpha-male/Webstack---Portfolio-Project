<!-- eslint-disable vue/html-closing-bracket-newline -->
<!-- eslint-disable @stylistic/semi -->
<!-- eslint-disable @stylistic/comma-dangle -->
<!-- eslint-disable @stylistic/quotes -->
<script setup lang="ts">
import { ref } from "vue";
const toast = useToast();
definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Add Blog Post",
});

const fields = ref([
  {
    name: "title",
    type: "text",
    label: "Title",
    placeholder: "Enter the blog title",
  },
  {
    name: "category",
    type: "select",
    label: "Category",
    placeholder: "Select a category",
    options: [
      "computer Science",
      "Technology",
      "Software Engneering",
      "Programming",
    ],
  },
  {
    name: "content",
    type: "textarea",
    label: "Content",
    placeholder: "Enter the blog content",
  },

  {
    name: "image",
    // type: "text",
    label: "Image",
    placeholder: "Enter the image URL",
    type: "file",
    multiple: true,
  },
]);
const state = ref({
  title: "",
  content: "",
  images: [] as File[],
  category: "",
});
const validate = () => {
  const errors = [];
  if (!state.value.title)
    errors.push({ path: "title", message: "Title is required" });
  if (!state.value.content)
    errors.push({ path: "content", message: "Content is required" });
  if (!state.value.category)
    errors.push({ path: "category", message: "Category is required" });
  return errors;
};

const onSubmit = async (data: any) => {
  const router = useRouter();

  console.log(data);

  try {
    const response = await fetch("http://127.0.0.1:8000/blogs/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
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
    <UAuthForm
      :fields="fields"
      :validate="validate"
      :providers="providers"
      align="top"
      title="Create a Blog Post"
      :ui="{ base: 'text-center', footer: 'text-center' }"
      :submit-button="{ label: 'addblog' }"
      @submit="onSubmit"
    >
    </UAuthForm>
  </UCard>
</template>
