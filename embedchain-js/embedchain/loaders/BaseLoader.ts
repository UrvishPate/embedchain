import type { Input, LoaderResult } from '../models';
/**
 * An abstract base class for loaders. 
 * Each loader should implement the loadData method.
 */
export abstract class BaseLoader {
  /**
   * Loads data from a given source.
   * 
   * @param src - The source from which to load data.
   * @returns A promise that resolves with the loaded data.
   */
  abstract loadData(src: Input): Promise<LoaderResult>;
}