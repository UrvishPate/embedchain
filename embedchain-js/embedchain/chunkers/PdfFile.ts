import { RecursiveCharacterTextSplitter } from 'langchain/text_splitter';
import { BaseChunker } from './BaseChunker';
interface TextSplitterChunkParams {
  chunkSize: number;
  chunkOverlap: number;
  keepSeparator: boolean;
}
const TEXT_SPLITTER_CHUNK_PARAMS: TextSplitterChunkParams = {
  chunkSize: 1000,
  chunkOverlap: 0,
  keepSeparator: false,
};
/**
 * Represents a PDF file chunker that extends the base chunker.
 */
class PdfFileChunker extends BaseChunker {
  /**
   * Creates a new PdfFileChunker.
   */
  constructor() {
    const textSplitter = new RecursiveCharacterTextSplitter(
      TEXT_SPLITTER_CHUNK_PARAMS
    );
    super(textSplitter);
  }
}
export { PdfFileChunker };