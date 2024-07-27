<script setup lang="ts">
const toast = useToast();
definePageMeta({
  layout: "auth",
});

useSeoMeta({
  title: "Login",
});

/**
 * @description: An array of fields for the login form.
 * @type: Array
 * @property {string} name - The name of the input field.
 * @property {string} type - The type of the input field.
 * @property {string} label - The label of the input field.
 * @property {string} placeholder - The placeholder text for the input field.
 */
const fields = [
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

/**
 * @description: A function that validates the form data before submitting the login request.
 * @param {Object} state - The state object containing the form data.
 * @returns {Array} An array of error objects, where each object contains the path and message.
 */
const validate = (state: any) => {
  const errors = [];
  if (!state.email)
    errors.push({ path: "email", message: "Email is required" });
  if (!state.password)
    errors.push({ path: "password", message: "Password is required" });
  return errors;
};

/**
 * @description: An array of providers for the login form.
 * @type: Array
 * @property {string} label - The label of the provider.
 * @property {string} icon - The icon of the provider.
 * @property {string} color - The color of the provider's button.
 * @property {Function} click - A function that gets called when the provider's button is clicked.
 */
const providers = [
  {
    label: "Continue with GitHub",
    icon: "i-simple-icons-github",
    color: "white" as const,
    click: () => {
      console.log("Redirect to GitHub");
    },
  },
];

/**
 * @description: An asynchronous function that handles the submission of the login form.
 * @param {Object} data - The form data containing the email and password.
 * @returns {Promise<void>} A Promise that resolves when the login process is completed.
 */
const onSubmitUserLogin = async (data) => {
  const router = useRouter();

  console.log(data);

  try {
    const response = await fetch("http://127.0.0.1:8000/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // Convert the data to JSON string
    });

    if (!response.ok) {
      // Handle error response
      const errorData = await response.json();
      console.error("Failed to login:", errorData.detail);
      toast.add({
        title: "Login failed",
        description: errorData.detail || "Invalid email or password.",
        timeout: 1000,
      });
      return;
    }

    const result = await response.json(); // Get the response JSON

    localStorage.setItem("access_token", result.access_token);

    await navigateTo({ path: "/home" });
    toast.add({
      title: "Logged in successfully",
      timeout: 1000,
    });
  } catch (error) {
    console.error("Error during fetch:", error);
    toast.add({
      title: "Login failed",
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
      title="Welcome back"
      align="top"
      icon="i-heroicons-lock-closed"
      :ui="{ base: 'text-center', footer: 'text-center' }"
      :submit-button="{ trailingIcon: 'i-heroicons-arrow-right-20-solid' }"
      @submit="onSubmitUserLogin"
    >
      <template #description>
        Don't have an account?
        <NuxtLink to="/signup" class="text-primary font-medium"
          >Sign up</NuxtLink
        >.
      </template>

      <template #password-hint>
        <NuxtLink to="/" class="text-primary font-medium"
          >Forgot password?</NuxtLink
        >
      </template>

      <template #footer>
        By signing in, you agree to our
        <NuxtLink to="/" class="text-primary font-medium"
          >Terms of Service</NuxtLink
        >.
      </template>
    </UAuthForm>
  </UCard>
</template>
