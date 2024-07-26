<!-- eslint-disable vue/html-closing-bracket-newline -->
<!-- eslint-disable @stylistic/semi -->
<!-- eslint-disable @stylistic/comma-dangle -->
<!-- eslint-disable @stylistic/quotes -->
<script setup lang="ts">
const toast = useToast();
definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Sign up",
});

const fields = [
  {
    name: "name",
    type: "text",
    label: "Name",
    placeholder: "Enter your name",
  },
  {
    name: "email",
    type: "text",
    label: "Email",
    placeholder: "Enter your email",
  },
  {
    name: "password",
    label: "Password",
    type: "password",
    placeholder: "Enter your password",
  },
];

const validate = (state: any) => {
  const errors = [];
  if (!state.email)
    errors.push({ path: "email", message: "Email is required" });
  if (!state.password)
    errors.push({ path: "password", message: "Password is required" });
  return errors;
};

const providers = [
  {
    label: "Continue with GitHub",
    icon: "i-simple-icons-github",
    color: "gray" as const,
    click: () => {
      console.log("Redirect to GitHub");
    },
  },
];

const onSubmit = async (data: any) => {
  const router = useRouter();

  console.log(data);

  try {
    const response = await fetch("http://127.0.0.1:8000/add_users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      // Handle error response
      const errorData = await response.json();
      console.error("Failed to add user:", errorData.detail);
      toast.add({
        title: "User creation failed",
        description:
          errorData.detail || "An error occurred while creating the user.",
        timeout: 1000,
      });
      return;
    }

    const result = await response.json(); // Get the response JSON
    console.log(result);
    await navigateTo({ path: "/login" });
    toast.add({
      title: "User created successfully",
      timeout: 1000,
    });
  } catch (error) {
    console.error("Error during fetch:", error);
    toast.add({
      title: "User creation failed",
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
      title="Create an account"
      :ui="{ base: 'text-center', footer: 'text-center' }"
      :submit-button="{ label: 'Create account' }"
      @submit="onSubmit"
    >
      <template #description>
        Already have an account?
        <NuxtLink to="/login" class="text-primary font-medium">Login</NuxtLink>.
      </template>

      <template #footer>
        By signing up, you agree to our
        <NuxtLink to="/" class="text-primary font-medium">
          Terms of Service </NuxtLink
        >.
      </template>
    </UAuthForm>
  </UCard>
</template>
