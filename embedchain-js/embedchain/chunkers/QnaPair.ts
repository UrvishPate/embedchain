import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { BaseChunker } from './BaseChunker';
interface TextSplitterChunkParams {
  chunkSize: number;
  chunkOverlap: number;
  keepSeparator: boolean;
}
const TEXT_SPLITTER_CHUNK_PARAMS: TextSplitterChunkParams = {
  chunkSize: 300,
  chunkOverlap: 0,
  keepSeparator: false,
};
/**
 * Represents a QnaPairChunker class that extends the BaseChunker class.
 */
class QnaPairChunker extends BaseChunker {
  /**
   * Constructs a new QnaPairChunker.
   * Initializes a new RecursiveCharacterTextSplitter with TEXT_SPLITTER_CHUNK_PARAMS and passes it to the constructor of the superclass.
   */
  constructor() {
    const textSplitter = new RecursiveCharacterTextSplitter(
      TEXT_SPLITTER_CHUNK_PARAMS
    );
    super(textSplitter);
  }
}
export { QnaPairChunker };