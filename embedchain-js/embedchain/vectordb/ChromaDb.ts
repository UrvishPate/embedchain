import type { Collection } from 'chromadb';
import { ChromaClient, OpenAIEmbeddingFunction } from 'chromadb';
import { BaseVectorDB } from './BaseVectorDb';
const embedder = new OpenAIEmbeddingFunction({
  openai_api_key: process.env.OPENAI_API_KEY ?? '',
});
/**
 * Represents a ChromaDB which extends BaseVectorDB.
 */
class ChromaDB extends BaseVectorDB {
  client: ChromaClient | undefined;

  collection: Collection | null = null;

  /**
   * Constructor for ChromaDB class.
   * @constructor
   */
  // eslint-disable-next-line @typescript-eslint/no-useless-constructor
  constructor() {
    super();
  }

  /**
   * Asynchronously gets the client and collection.
   * @method
   * @returns {Promise<void>} - A promise that resolves when the client and collection are obtained.
   */
  protected async getClientAndCollection(): Promise<void> {
    this.client = new ChromaClient({ path: 'http://localhost:8000' });
    try {
      this.collection = await this.client.getCollection({
        name: 'embedchain_store',
        embeddingFunction: embedder,
      });
    } catch (err) {
      if (!this.collection) {
        this.collection = await this.client.createCollection({
          name: 'embedchain_store',
          embeddingFunction: embedder,
        });
      }
    }
  }
}
export { ChromaDB };