export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import BookingsClient from "./BookingsClient";

export default async function BookingsPage() {
  const bookings = await fetchAPI("/bookings").catch(() => []);
  const mechanics = await fetchAPI("/mechanics").catch(() => []);
  const spareparts = await fetchAPI("/spareparts").catch(() => []);
  return <BookingsClient bookings={JSON.parse(JSON.stringify(bookings))} mechanics={JSON.parse(JSON.stringify(mechanics))} spareparts={JSON.parse(JSON.stringify(spareparts))} />;
}
