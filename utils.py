def flip_animation(animation_obj, flipX, flipY):
        flipped_obj = animation_obj.getCopy()
        flipped_obj.flip(flipX, flipY)
        flipped_obj.makeTransformsPermanent()
        return flipped_obj