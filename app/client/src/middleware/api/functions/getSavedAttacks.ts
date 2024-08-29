import { restGet } from "../../rest-calls/rest-get";
import type { Attack } from "../../../../../types/client-types";

export async function getSavedAttacks(): Promise<Attack[] | null> {
  try {
    const fetchedData = await restGet("/client/saved_attacks");
    console.log(fetchedData);
    return fetchedData as Attack[];
  } catch (error) {
    console.error("Error fetching saved attacks:", error);
    return null;
  }
}
