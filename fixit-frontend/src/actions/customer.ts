"use server";
import { fetchAPI } from "@/lib/api";
import { revalidatePath } from "next/cache";
import { auth } from "@/lib/auth";

export async function simulatePayment(invoiceId: number) {
  const session = await auth();
  if (!session?.user) throw new Error("Not authenticated");

  // Verify the invoice belongs to the user
  const invoice = await fetchAPI(`/invoices/${invoiceId}`);

  if (!invoice || invoice.booking.userId !== Number(session.user.id)) {
    throw new Error("Unauthorized");
  }

  await fetchAPI(`/invoices/${invoiceId}`, { method: "PUT", body: JSON.stringify({ ...invoice, paymentStatus: "PAID", paymentMethod: "TRANSFER", paidAt: new Date().toISOString() }) });

  revalidatePath("/my/invoices");
  return { success: true };
}
