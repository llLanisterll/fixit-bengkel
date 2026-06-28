"use server";
import { fetchAPI } from "@/lib/api";
import { revalidatePath } from "next/cache";
import bcrypt from "bcryptjs";
import { auth } from "@/lib/auth";

export async function updateProfile(data: { name: string; phone: string; password?: string }) {
  const session = await auth();
  if (!session?.user) return { error: "Not authenticated" };
  
  const updateData: any = { name: data.name, phone: data.phone };
  
  if (data.password) {
    updateData.password = await bcrypt.hash(data.password, 10);
  }
  
  const user = await fetchAPI(`/users/${session.user.id}`);
  await fetchAPI(`/users/${session.user.id}`, { method: "PUT", body: JSON.stringify({ ...user, ...updateData }) });
  
  revalidatePath("/my/profile");
  return { success: true };
}
