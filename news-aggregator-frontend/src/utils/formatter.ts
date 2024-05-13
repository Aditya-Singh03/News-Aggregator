import { format } from "date-fns";

export function linkFormatter(linkString: string) {
  return new URL(linkString).hostname;
}

export function dateFormatter(dateString: string) {
  return format(dateString, "yyyy-MM-dd'T'kk:mm:ss'Z'").split("T")[0];
}

export function nameFormatter(name: string) {
  return name
    .toLowerCase()
    .split(" ")
    .map((word) => capitalize(word))
    .join(" ");
}

export function minimizeSummary(summary: string) {
  return summary.split("").reduce(
    (acc, e) => {
      if (acc.charCount < 220) {
        acc.charCount++;
        acc.text += e;
      }
      return acc;
    },
    { text: "", charCount: 0 }
  ).text + "...";
}

function capitalize(word: string) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}
