export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import ServicesClient from "./ServicesClient";
export default async function ServicesPage() {
  const services = await fetchAPI("/services").catch(() => []);
  return <ServicesClient services={JSON.parse(JSON.stringify(services))} />;
}
