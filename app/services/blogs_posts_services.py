def generate_post(prompt: str, current_user: str, db: Session):

    # 1. Generar contenido con IA
    result = generar_blog(prompt)
    print(f"json: {result}")

    # 2. Validar JSON
    try:
        json_data = json.loads(result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"La IA no devolvió un JSON válido: {e}"
        )

    # 3. Mapear claves del JSON a columnas correctas de tu modelo
    post = Article(
        id=json_data.get("id"),
        title=json_data.get("title"),
        description=json_data.get("description"),
        image_url=json_data.get("imageurl"),      # <- aquí ajustado
        date_creation=json_data.get("datecreation"),  # <- aquí ajustado
        autor_id=current_user                     # <- tu modelo usa autor_id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return {
        "message": "Artículo generado y guardado correctamente",
        "post": post.to_dict()
    }
