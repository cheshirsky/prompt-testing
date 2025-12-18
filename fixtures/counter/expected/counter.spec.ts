import { increment } from './counter';

describe('increment', () => {
  it('should return 1 when given 0', () => {
    // Arrange
    const input = 0;

    // Act
    const result = increment(input);

    // Assert
    expect(result).toBe(1);
  });

  it('should return 6 when given 5', () => {
    // Arrange
    const input = 5;

    // Act
    const result = increment(input);

    // Assert
    expect(result).toBe(6);
  });

  it('should return 0 when given -1', () => {
    // Arrange
    const input = -1;

    // Act
    const result = increment(input);

    // Assert
    expect(result).toBe(0);
  });
});
