"use server";
import { signIn, signOut } from "@/lib/auth";
import { redirect } from "next/navigation";
import { fetchAPI } from "@/lib/api";

export async function loginAction(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;
  try {
    const result = await signIn("credentials", { email, password, redirect: false });
    if (result?.error) return { error: "Email atau password salah" };
  } catch {
    return { error: "Email atau password salah" };
  }

  // To check if they are admin, we can decode the token or just fetch user details if needed.
  // Actually, next-auth session handles redirect based on role in Next.js middleware or we can just redirect to dashboard, and middleware will handle it.
  // But let's check role from token directly if possible. Since we can't easily, let's just use NextAuth's auth()
  const { auth } = await import("@/lib/auth");
  const session = await auth();
  if (session?.user?.role === "ADMIN") redirect("/dashboard");
  
  redirect("/my/dashboard");
}

export async function registerAction(formData: FormData) {
  const name = formData.get("name") as string;
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;
  const phone = formData.get("phone") as string;
  
  if (!name || !email || !password) return { error: "Semua field harus diisi" };
  
  try {
    await fetchAPI("/auth/register", {
      method: "POST",
      body: JSON.stringify({ name, email, password, phone }),
    });
  } catch (err: any) {
    return { error: err.message || "Email sudah terdaftar atau terjadi kesalahan" };
  }
  
  try {
    await signIn("credentials", { email, password, redirect: false });
  } catch { /* ignore */ }
  redirect("/my/dashboard");
}

export async function logoutAction() {
  await signOut({ redirect: false });
  redirect("/login");
}
