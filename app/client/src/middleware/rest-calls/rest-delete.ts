import { baseUrl } from "../../lib/utils";
export async function restDelete(
  path: string,
  message: string
): Promise<boolean> {
  try {
    const response = await fetch(baseUrl + path, {
      method: "DELETE",
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
