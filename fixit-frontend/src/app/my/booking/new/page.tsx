export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import BookingForm from "./BookingForm";

export default async function NewBookingPage() {
  const session = await auth();
  if (!session?.user) redirect("/login");
  const userId = Number(session.user.id);
    const allVehicles = await fetchAPI("/vehicles").catch(() => []);
  const allServices = await fetchAPI("/services").catch(() => []);
  const allMechanics = await fetchAPI("/mechanics").catch(() => []);
  
  const vehicles = allVehicles.filter((v: any) => v.userId === userId);
  const services = allServices.filter((s: any) => s.isActive).sort((a: any, b: any) => a.category.localeCompare(b.category));
  const mechanics = allMechanics.filter((m: any) => m.status === "AVAILABLE");
  return <BookingForm vehicles={JSON.parse(JSON.stringify(vehicles))} services={JSON.parse(JSON.stringify(services))} mechanics={JSON.parse(JSON.stringify(mechanics))} userId={userId} />;
}
