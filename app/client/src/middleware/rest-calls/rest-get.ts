import { baseUrl } from "../../lib/utils";

export async function restGet(path: string) {
  try {
    console.log(baseUrl, "- ", path);
    const response = await fetch(baseUrl + path, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
}
