import { jsPDF } from "jspdf";
import { SARABUN_REGULAR_BASE64 } from "./sarabun-regular-base64";
import { SARABUN_BOLD_BASE64 } from "./sarabun-bold-base64";

/**
 * Register Sarabun fonts (Thai) to a jsPDF document instance.
 * Uses pre-encoded base64 data so no runtime fetch is needed.
 * Returns true if fonts were registered successfully.
 */
export function registerSarabunFont(doc: jsPDF): boolean {
    try {
        doc.addFileToVFS("Sarabun-Regular.ttf", SARABUN_REGULAR_BASE64);
        doc.addFont("Sarabun-Regular.ttf", "Sarabun", "normal");

        doc.addFileToVFS("Sarabun-Bold.ttf", SARABUN_BOLD_BASE64);
        doc.addFont("Sarabun-Bold.ttf", "Sarabun", "bold");

        // Verify registration by setting the font
        doc.setFont("Sarabun", "normal");
        return true;
    } catch (error) {
        console.error("Failed to register Sarabun fonts:", error);
        return false;
    }
}
