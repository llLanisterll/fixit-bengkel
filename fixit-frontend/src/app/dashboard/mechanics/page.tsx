export const dynamic = "force-dynamic";
import { fetchAPI } from "@/lib/api";
import MechanicsClient from "./MechanicsClient";

export default async function MechanicsPage() {
  const mechanics = await fetchAPI("/mechanics").catch(() => []);
  return <MechanicsClient mechanics={JSON.parse(JSON.stringify(mechanics))} />;
}
