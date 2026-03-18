import time

def zigzag_recursion(depth, limit):
    """
    A visualizer for the 'Zigzag Paper' analogy of recursion.
    
    'Holding the left end' = Each call waiting for the next.
    'Moving until limit' = Recursive calls descending.
    'Flying back' = Unwinding the stack.
    """
    indent = "  " * depth
    
    # 1. THE WINDING PHASE (Holding the left end, moving the right)
    if depth == 0:
        print(f"\n[START] Holding the left end of the paper stripe...")
    
    print(f"{indent}>>> Calling depth {depth} (Stretching the stripe...)")
    time.sleep(0.3)  # Slow down for visual effect

    # 2. BASE CASE (The limit of the paper)
    if depth >= limit:
        print(f"{indent}!!! LIMIT REACHED at depth {depth}. Releasing the left end!")
        return f"Result_{depth}"

    # 3. THE RECURSIVE STEP (The Leap of Faith)
    # This is where we 'wait' while the next part stretches
    child_result = zigzag_recursion(depth + 1, limit)

    # 4. THE UNWINDING PHASE (The snapback)
    print(f"{indent}<<< Back at depth {depth}. Received: {child_result}. (Stripe snapping back...)")
    time.sleep(0.3)
    
    return f"Result_{depth} + {child_result}"

if __name__ == "__main__":
    print("--- RECURSION VISUALIZER: THE ZIGZAG STRIPE ---")
    final_snap = zigzag_recursion(0, 4)
    print(f"\n[FINISH] The stripe has fully snapped back. Final string: {final_snap}")
