import type { LoaderResult, QnaPair } from '../models';
import { BaseLoader } from './BaseLoader';
/**
 * Class representing a local Q&A pair loader.
 * This class extends the BaseLoader class.
 */
class LocalQnaPairLoader extends BaseLoader {
  /**
   * Load data from a Q&A pair.
   * This method is asynchronous.
   *
   * @param content - A Q&A pair.
   * @returns A promise that resolves to a LoaderResult.
   */
  // eslint-disable-next-line class-methods-use-this
  async loadData(content: QnaPair): Promise<LoaderResult> {
    const [question, answer] = content;
    const contentText = `Q: ${question}\nA: ${answer}`;
    const metaData = {
      url: 'local',
    };
    return [
      {
        content: contentText,
        metaData,
      },
    ];
  }
}
export { LocalQnaPairLoader };