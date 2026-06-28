"use server";
import { revalidatePath } from "next/cache";
import { auth } from "@/lib/auth";
import { fetchAPI } from "@/lib/api";

async function requireAuth() {
  const session = await auth();
  if (!session?.user) throw new Error("Unauthorized");
  return session;
}

export async function updateBookingStatus(bookingId: number, status: string, mechanicId?: number) {
  const session = await requireAuth();
  if (session.user.role !== "ADMIN") throw new Error("Unauthorized");
  
  const payload: any = { status, userId: 1, vehicleId: 1, bookingDate: new Date().toISOString(), timeSlot: "" }; // dummy required fields for PUT if FastAPI schema requires them, wait, we can just use PUT to update. Actually FastAPI update_booking requires schemas.BookingCreate, which might need all fields. Let's fetch the existing booking first.
  
  const existing = await fetchAPI(`/bookings/${bookingId}`);
  await fetchAPI(`/bookings/${bookingId}`, {
    method: "PUT",
    body: JSON.stringify({
      ...existing,
      status,
      mechanicId: mechanicId || existing.mechanicId
    }),
  });
  
  if (mechanicId) {
    const mech = await fetchAPI(`/mechanics/${mechanicId}`);
    await fetchAPI(`/mechanics/${mechanicId}`, {
      method: "PUT",
      body: JSON.stringify({ ...mech, status: status === "IN_PROGRESS" ? "BUSY" : "AVAILABLE" }),
    });
  }
  
  revalidatePath("/dashboard/bookings");
  revalidatePath("/my/bookings");
}

export async function createBooking(data: { userId: number; vehicleId: number; mechanicId?: number; bookingDate: string; timeSlot: string; notes?: string; serviceIds: number[] }) {
  await requireAuth();
  
  const booking = await fetchAPI("/bookings", {
    method: "POST",
    body: JSON.stringify(data),
  });

  revalidatePath("/my/bookings");
  revalidatePath("/dashboard/bookings");
  return booking;
}

export async function cancelBooking(bookingId: number) {
  await requireAuth();
  const existing = await fetchAPI(`/bookings/${bookingId}`);
  const booking = await fetchAPI(`/bookings/${bookingId}`, {
    method: "PUT",
    body: JSON.stringify({ ...existing, status: "CANCELLED" })
  });
  
  if (booking.mechanicId) {
    const mech = await fetchAPI(`/mechanics/${booking.mechanicId}`);
    await fetchAPI(`/mechanics/${booking.mechanicId}`, {
      method: "PUT",
      body: JSON.stringify({ ...mech, status: "AVAILABLE" })
    });
  }
  
  revalidatePath("/my/bookings");
  revalidatePath("/dashboard/bookings");
}
