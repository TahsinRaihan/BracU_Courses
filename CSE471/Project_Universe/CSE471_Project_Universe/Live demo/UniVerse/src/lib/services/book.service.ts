import { BookRepository } from "$lib/repositories/book.repository";
import type { Book } from "$lib/types/book";

export class BookService {
  private bookRepository: BookRepository;

  constructor() {
    this.bookRepository = new BookRepository();
  }

  async getAllBooks(): Promise<Book[]> {
    try {
      return await this.bookRepository.getAllBooks();
    } catch (error) {
      console.error("Error fetching all books:", error);
      throw new Error("Failed to retrieve books");
    }
  }

  async getBookById(id: string): Promise<Book | null> {
    try {
      if (!id) {
        throw new Error("Book ID is required");
      }
      return await this.bookRepository.getBookById(id);
    } catch (error) {
      console.error("Error fetching book by ID:", error);
      throw new Error("Failed to retrieve book");
    }
  }

  async searchBooks(query: string): Promise<Book[]> {
    try {
      if (!query || query.trim().length === 0) {
        return await this.getAllBooks();
      }
      return await this.bookRepository.searchBooks(query.trim());
    } catch (error) {
      console.error("Error searching books:", error);
      throw new Error("Failed to search books");
    }
  }

  async getAvailableBooks(): Promise<Book[]> {
    try {
      return await this.bookRepository.getBooksByStatus("available");
    } catch (error) {
      console.error("Error fetching available books:", error);
      throw new Error("Failed to retrieve available books");
    }
  }

  async getBookAvailabilityStatus(id: string): Promise<Book["status"] | null> {
    try {
      const book = await this.bookRepository.getBookById(id);
      return book?.status || null;
    } catch (error) {
      console.error("Error fetching book availability:", error);
      throw new Error("Failed to retrieve book availability");
    }
  }
}
