import { baseUrl } from "../../lib/utils";

export async function restPut(path: string, message: string): Promise<boolean> {
  try {
    const response = await fetch(baseUrl + path, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: message,
    });
    if (response.ok) {
      if (response.status === 500) {
        return false;
      }
      return true;
    }
    return false;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}
