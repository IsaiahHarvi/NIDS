import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const baseUrl = "/api/v1";

export const parseData = (date: string | Date): Date => {
  return date instanceof Date ? date : new Date(date);
};
