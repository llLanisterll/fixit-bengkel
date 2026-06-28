"use server";
import { fetchAPI } from "@/lib/api";
import { revalidatePath } from "next/cache";
import { auth } from "@/lib/auth";

async function requireAuth() {
  const session = await auth();
  if (!session?.user) throw new Error("Unauthorized");
}

export async function createVehicle(data: { userId: number; brand: string; model: string; year: number; licensePlate: string; color?: string }) {
  await requireAuth();
  await fetchAPI("/vehicles", { method: "POST", body: JSON.stringify(data) });
  revalidatePath("/my/vehicles");
}

export async function updateVehicle(id: number, data: { brand: string; model: string; year: number; licensePlate: string; color?: string }) {
  await requireAuth();
  const v = await fetchAPI(`/vehicles/${id}`); await fetchAPI(`/vehicles/${id}`, { method: "PUT", body: JSON.stringify({ ...v, ...data }) });
  revalidatePath("/my/vehicles");
}

export async function deleteVehicle(id: number) {
  await requireAuth();
  await fetchAPI(`/vehicles/${id}`, { method: "DELETE" });
  revalidatePath("/my/vehicles");
}
