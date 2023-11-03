import { createHash } from 'crypto';
import type { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import type { BaseLoader } from '../loaders';
import type { Input, LoaderResult } from '../models';
import type { ChunkResult } from '../models/ChunkResult';
/**
 * A class that represents a base chunker.
 * This class is responsible for creating chunks of data.
 */
class BaseChunker {
  textSplitter: RecursiveCharacterTextSplitter;

  /**
   * Creates a new BaseChunker instance.
   *
   * @param textSplitter - An instance of RecursiveCharacterTextSplitter.
   */
  constructor(textSplitter: RecursiveCharacterTextSplitter) {
    this.textSplitter = textSplitter;
  }

  /**
   * Creates chunks of data from a given url.
   *
   * @param loader - An instance of BaseLoader.
   * @param url - The url to load data from.
   * @returns A promise that resolves to an object containing arrays of documents, ids, and metadatas.
   */
  async createChunks(loader: BaseLoader, url: Input): Promise<ChunkResult> {
    const documents: ChunkResult['documents'] = [];
    const ids: ChunkResult['ids'] = [];
    const datas: LoaderResult = await loader.loadData(url);
    const metadatas: ChunkResult['metadatas'] = [];

    const dataPromises = datas.map(async (data) => {
      const { content, metaData } = data;
      const chunks: string[] = await this.textSplitter.splitText(content);
      chunks.forEach((chunk) => {
        const chunkId = createHash('sha256')
          .update(chunk + metaData.url)
          .digest('hex');
        ids.push(chunkId);
        documents.push(chunk);
        metadatas.push(metaData);
      });
    });

    await Promise.all(dataPromises);

    return {
      documents,
      ids,
      metadatas,
    };
  }
}
export { BaseChunker };