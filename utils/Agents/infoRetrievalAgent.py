from Project.StyleMatch.utils.Templates.schemas import ImageState
import faiss
import json
from PIL import Image
import numpy as np
from utils.models.clipModel import clip_model


class InfoRetrievalAgent:
    def __init__(self, index_path: str, metadata_path: str):
        self.index = faiss.read_index(index_path)
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)

    def retrieve_similar_items(self, imageState: ImageState, top_k: int = 5) -> dict:
        segmented_imgs = imageState.segmented_imgs

        embeddings_segments = [clip_model.encode(img) for img in segmented_imgs]
        embeddings_segments = np.array(embeddings_segments).astype('float32')

        dist_indices = [self.index.search(embedding[np.newaxis, :], top_k) for embedding in embeddings_segments]

        results = {}
        for seg_idx, (distances, indices) in enumerate(dist_indices):
            seg_results = []
            for dist, idx in zip(distances[0], indices[0]):
                item_metadata = self.metadata[str(idx)]
                seg_results.append({
                    'metadata': item_metadata,
                    'distance': float(dist)
                })
            results[f'segment_{seg_idx}'] = seg_results

        return {
            'results': results
        }