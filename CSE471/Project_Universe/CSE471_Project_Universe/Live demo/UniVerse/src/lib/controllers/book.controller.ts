import { BookService } from "$lib/services/book.service";
import type { Book } from "$lib/types/book";

export class BookController {
  private bookService: BookService;

  constructor() {
    this.bookService = new BookService();
  }

  async getAllBooks(): Promise<{ success: boolean; data?: Book[]; error?: string }> {
    try {
      const books = await this.bookService.getAllBooks();
      return {
        success: true,
        data: books
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Failed to fetch books"
      };
    }
  }

  async getBookById(id: string): Promise<{ success: boolean; data?: Book; error?: string }> {
    try {
      const book = await this.bookService.getBookById(id);
      if (!book) {
        return {
          success: false,
          error: "Book not found"
        };
      }
      return {
        success: true,
        data: book
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Failed to fetch book"
      };
    }
  }

  async searchBooks(query: string): Promise<{ success: boolean; data?: Book[]; error?: string }> {
    try {
      const books = await this.bookService.searchBooks(query);
      return {
        success: true,
        data: books
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Failed to search books"
      };
    }
  }

  async getAvailableBooks(): Promise<{ success: boolean; data?: Book[]; error?: string }> {
    try {
      const books = await this.bookService.getAvailableBooks();
      return {
        success: true,
        data: books
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Failed to fetch available books"
      };
    }
  }

  async getBookAvailabilityStatus(id: string): Promise<{ success: boolean; data?: Book["status"]; error?: string }> {
    try {
      const status = await this.bookService.getBookAvailabilityStatus(id);
      if (status === null) {
        return {
          success: false,
          error: "Book not found"
        };
      }
      return {
        success: true,
        data: status
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Failed to fetch book availability"
      };
    }
  }
}
