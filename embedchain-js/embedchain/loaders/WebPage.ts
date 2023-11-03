import axios from 'axios';
import { JSDOM } from 'jsdom';
import { cleanString } from '../utils';
import { BaseLoader } from './BaseLoader';
/**
 * Class representing a WebPageLoader.
 * @extends BaseLoader
 */
class WebPageLoader extends BaseLoader {
  /**
   * Load data from a specific URL and clean the HTML content by removing unwanted tags.
   * 
   * @param {string} url - The URL to load data from.
   * @returns {Array} output - An array containing the cleaned content and metadata of the webpage.
   * @throws Will throw an error if the web page content is empty.
   */
  // eslint-disable-next-line class-methods-use-this
  async loadData(url: string) {
    const response = await axios.get(url);
    const html = response.data;
    const dom = new JSDOM(html);
    const { document } = dom.window;
    const unwantedTags = [
      'nav',
      'aside',
      'form',
      'header',
      'noscript',
      'svg',
      'canvas',
      'footer',
      'script',
      'style',
    ];
    unwantedTags.forEach((tagName) => {
      const elements = document.getElementsByTagName(tagName);
      Array.from(elements).forEach((element) => {
        // eslint-disable-next-line no-param-reassign
        (element as HTMLElement).textContent = ' ';
      });
    });

    const output = [];
    let content = document.body.textContent;
    if (!content) {
      throw new Error('Web page content is empty.');
    }
    content = cleanString(content);
    const metaData = {
      url,
    };
    output.push({
      content,
      metaData,
    });
    return output;
  }
}
export { WebPageLoader };