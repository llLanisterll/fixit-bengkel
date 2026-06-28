export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import { auth } from "@/lib/auth";
import { redirect } from "next/navigation";
import VehiclesClient from "./VehiclesClient";

export default async function VehiclesPage() {
  const session = await auth();
  if (!session?.user) redirect("/login");
  const userId = Number(session.user.id);
  const allVehicles = await fetchAPI("/vehicles").catch(() => []);
  const vehicles = allVehicles.filter((v: any) => v.userId === userId);
  return <VehiclesClient vehicles={JSON.parse(JSON.stringify(vehicles))} userId={userId} />;
}
