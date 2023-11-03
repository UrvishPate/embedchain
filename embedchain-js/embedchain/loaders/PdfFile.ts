import type { TextContent } from 'pdfjs-dist/types/src/display/api';
import type { LoaderResult, Metadata } from '../models';
import { cleanString } from '../utils';
import { BaseLoader } from './BaseLoader';
const pdfjsLib = require('pdfjs-dist');
interface Page {
  page_content: string;
}
/**
 * Class representing a PDF File Loader.
 * This class extends the BaseLoader class.
 */
class PdfFileLoader extends BaseLoader {
  /**
   * Asynchronously gets pages from a PDF file.
   * 
   * @param {string} url - The URL of the PDF file.
   * @returns {Promise<Page[]>} - A promise that resolves with an array of pages.
   */
  static async getPagesFromPdf(url: string): Promise<Page[]> {
    const loadingTask = pdfjsLib.getDocument(url);
    const pdf = await loadingTask.promise;
    const { numPages } = pdf;

    const promises = Array.from({ length: numPages }, async (_, i) => {
      const page = await pdf.getPage(i + 1);
      const pageText: TextContent = await page.getTextContent();
      const pageContent: string = pageText.items
        .map((item) => ('str' in item ? item.str : ''))
        .join(' ');

      return {
        page_content: pageContent,
      };
    });

    return Promise.all(promises);
  }

  /**
   * Asynchronously loads data from a URL.
   * 
   * @param {string} url - The URL to load data from.
   * @returns {Promise<LoaderResult>} - A promise that resolves with the loaded data.
   * @throws {Error} - Throws an error if no data is found.
   */
  // eslint-disable-next-line class-methods-use-this
  async loadData(url: string): Promise<LoaderResult> {
    const pages: Page[] = await PdfFileLoader.getPagesFromPdf(url);
    const output: LoaderResult = [];

    if (!pages.length) {
      throw new Error('No data found');
    }

    pages.forEach((page) => {
      let content: string = page.page_content;
      content = cleanString(content);
      const metaData: Metadata = {
        url,
      };
      output.push({
        content,
        metaData,
      });
    });
    return output;
  }
}
export { PdfFileLoader };