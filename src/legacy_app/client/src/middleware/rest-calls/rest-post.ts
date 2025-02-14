import { baseUrl } from "../../lib/utils";

export async function restPost(
  path: string,
  message: string
): Promise<boolean> {
  try {
    const response = await fetch(baseUrl + path, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: message,
    });
    if (response.ok) {
      if (response.status === 500) {
        return false;
      }
      const body = await response.json();
      if (body.status === 400) {
        console.error("Bad data: POST " + path);
        return false;
      }
      return true;
    }
    console.log("Not Ok!");
    return false;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}
