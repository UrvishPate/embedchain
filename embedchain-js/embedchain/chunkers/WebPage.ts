import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { BaseChunker } from './BaseChunker';
interface TextSplitterChunkParams {
  chunkSize: number;
  chunkOverlap: number;
  keepSeparator: boolean;
}
const TEXT_SPLITTER_CHUNK_PARAMS: TextSplitterChunkParams = {
  chunkSize: 500,
  chunkOverlap: 0,
  keepSeparator: false,
};
/**
 * Represents a WebPageChunker that extends BaseChunker.
 * It uses RecursiveCharacterTextSplitter for splitting the text.
 */
class WebPageChunker extends BaseChunker {
  /**
   * Constructs a new WebPageChunker.
   * Initializes a new RecursiveCharacterTextSplitter with TEXT_SPLITTER_CHUNK_PARAMS and passes it to the BaseChunker constructor.
   */
  constructor() {
    const textSplitter = new RecursiveCharacterTextSplitter(
      TEXT_SPLITTER_CHUNK_PARAMS
    );
    super(textSplitter);
  }
}
export { WebPageChunker };