export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import BookingsListClient from "./BookingsListClient";

export default async function BookingsPage() {
  const session = await auth();
  if (!session?.user) redirect("/login");
  const userId = Number(session.user.id);
  const allBookings = await fetchAPI("/bookings").catch(() => []);
  const bookings = allBookings.filter((b: any) => b.userId === userId);
  return <BookingsListClient bookings={JSON.parse(JSON.stringify(bookings))} />;
}
