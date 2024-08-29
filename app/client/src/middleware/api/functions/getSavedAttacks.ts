import { restGet } from "../../rest-calls/rest-get";
import type { Attack } from "../../../../../types/client-types";

export async function getSavedAttacks(): Promise<Attack[] | null> {
  try {
    const fetchedData = await restGet("/saved_attacks");
    return fetchedData as Attack[];
  } catch (error) {
    console.error("Error fetching saved attacks:", error);
    return null;
  }
}
